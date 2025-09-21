
export class HttpError extends Error {
    statusCode: number;
    errors: Record<string, string[]>;

    constructor(statusCode: number, errors: Record<string, string[]>){
        super()
        this.statusCode = statusCode
        this.errors = errors
    }

    static fromJson(json: any, statusCode: number){
        let error = new HttpError(statusCode, json.errors)
        return error
    }   
}
