export class HttpResponse {
    data?: Record<string, any>|Record<string, any>[];
    total?: number;
    links?: Record<string, string>;
    current?: number;

    static fromJson(json: any){
        let response = new HttpResponse()
        response.data = json.data
        response.total = json.total
        response.links = json.links
        response.current = json.current
        return response
    }
}