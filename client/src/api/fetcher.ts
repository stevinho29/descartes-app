import { HttpResponse } from "../models/response";
import { HttpError } from "../models/error";


export async function call(url:string | URL, requestInit:RequestInit){
    return fetch(url, requestInit).then((response: Response) => {
        if (response.ok) {
          return response.json().then((json) => {
            return HttpResponse.fromJson(json);
          });
        } else {
          return response.json().then((json) => {
            throw HttpError.fromJson(json, response.status);
          });
        }
      }).catch((err) => {
        console.log(err)
        if (err instanceof HttpError)
          throw err
        throw new HttpError(500, {});
      });
}

export async function callIgnore404(url: string | URL, requestInit: RequestInit) {

    return fetch(url, requestInit).then((response: Response) => {
      if (response.ok) {
        return response.json().then((json) => {
          return HttpResponse.fromJson(json);
        });
      } else {
        return response.json().then((json) => {
          if (response.status === 404){
            return HttpResponse.fromJson({
                data: [],
                links: null,
                total: 0,
                current: null,
              });
          }
          throw HttpError.fromJson(json, response.status);
        });
      }
    }).catch((err) => {
      if (err instanceof HttpError)
        throw err
      throw new HttpError(500, {});
    });

  }

  export async function makeRequest(
    url: string | URL,
    body: File | FormData | URLSearchParams | string | null,
    method: string,
    headers: Headers | undefined
  ) {
    let requestInit: RequestInit = {
      method: method,
      body: body,
      headers: headers,
    };
    return call(url, requestInit);
  }

  export async function makeRequestIgnore404(
    url: string | URL,
    body: File | FormData | URLSearchParams | string | null,
    method: string,
    headers: Headers | undefined
  ) {
    let requestInit: RequestInit = {
      method: method,
      body: body,
      headers: headers,
    };
    return callIgnore404(url, requestInit);
  }

  export function makeUrl(url: string, params: any) {
    if (params) return new URL(url) + `?${new URLSearchParams(params).toString()}`;
    return new URL(url);
  }

  export function getHeaders(
    content_type: "application/json" | "multipart/form-data" | null,
  ): Headers {
    let headers = new Headers();
    if (content_type) headers.set("Content-Type", content_type);
    return headers;
  }