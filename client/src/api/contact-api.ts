import { ContactModel } from "@/models/contact";
import { makeRequest, makeRequestIgnore404, makeUrl } from "./fetcher";


export async function getContacts(params:Record<string, any>){
    const baseUrl = process.env.REACT_APP_BACKEND_URL
    console.log(baseUrl)
    const url = makeUrl(`${baseUrl}`, params);
    return makeRequestIgnore404(url, null, "GET", undefined).then((response) => {
      return response;
    });
}

export async function getContact(id:string){
    const baseUrl = process.env.REACT_APP_BACKEND_URL
    const url = makeUrl(`${baseUrl}/${id}`, null);
    return makeRequest(url, null, "GET", undefined).then((response) => {
      return response.data as ContactModel;
    });
}

export async function createContact(params:Record<string, any>){
    const baseUrl = process.env.REACT_APP_BACKEND_URL
    const url = makeUrl(`${baseUrl}`, null);
    return makeRequest(url, JSON.stringify(params), "POST", undefined).then((response) => {
      return response.data as ContactModel;
    });
}

export async function updateContact(id:string, params:Record<string, any>){
    const baseUrl = process.env.REACT_APP_BACKEND_URL
    const url = makeUrl(`${baseUrl}/${id}`, null);
    return makeRequest(url, JSON.stringify(params), "PUT", undefined).then((response) => {
      return response.data as ContactModel;
    });
}

export async function deleteContact(id:string){
    const baseUrl = process.env.REACT_APP_BACKEND_URL
    const url = makeUrl(`${baseUrl}/${id}`, null);
    return makeRequest(url, null, "DELETE", undefined).then((response) => {
      return response.data;
    });
}

export async function getEmailAddresses(params:Record<string, any>){
    const baseUrl = process.env.REACT_APP_BACKEND_URL
    const url = makeUrl(`${baseUrl}`, params);
    return makeRequestIgnore404(url, null, "GET", undefined).then((response) => {
      return response;
    });
}