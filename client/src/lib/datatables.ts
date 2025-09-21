import { SortingState } from "@tanstack/react-table";

type DatatablePageInfo = {
    sizePerPage: number;
    totalPages: number;
    currentPage: number;

}

export function getDatatablePageInfo(range: string, total: number) {
    const sizePerPage = parseInt(range.split("-")[1]) - parseInt(range.split("-")[0])
    const totalPages = Math.ceil(total / sizePerPage)
    const currentPage = parseInt(range.split("-")[1]) / sizePerPage - 1
    const info: DatatablePageInfo = {
        sizePerPage: sizePerPage,
        totalPages: totalPages,
        currentPage: currentPage
    }
    return info
}

export function getDatatableSortingState(sort: string[], desc: string[]) {
    let state = []
    for (let column of sort) {
        if (desc.includes(column))
            state.push({ "id": column, "desc": true })
        else
            state.push({ "id": column, "desc": false })
    }
    return state
}

export function getRange(pageIndex: number, pageSize: number) {
    return `${(pageIndex) * pageSize}-${(pageIndex + 1) * pageSize}`
}

export function getSortAndDesc(SortingState: SortingState){
    console.log(SortingState)
    let sort = []
    let desc = []
    for (let column of SortingState){
        sort.push(column["id"])
        if (column["desc"])
            desc.push(column["id"])
    }
    return {
        sort,
        desc
    }
}