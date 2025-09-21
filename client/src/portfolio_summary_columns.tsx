import { ColumnDef } from "@tanstack/react-table";
import { ContactModel } from "./models/contact";


export function getPortfolioSummaryColumns(onJobClickHandler: (value:string)=>void){
    const portfolioColumns: ColumnDef<ContactModel>[] = [
        {
          accessorKey: "first_name",
          header: "first name",
          enableSorting: true,
          cell: ({ row }) => {
            return <a href={`form/${row.original.id}`}>{row.original.first_name}</a>;
          },
        },
        {
            accessorKey: "last_name",
            header: "last name",
            enableSorting: false
        },
        {
            accessorKey: "email",
            header: "Email",
            enableSorting: false
        },
        {
          accessorKey: "job",
          header: "Job",
          enableSorting: true,
          cell: ({ row }) => {
            return <div 
            className="font-bold"
            onClick={()=>onJobClickHandler(row.original.job)}>{row.original.job}
            </div>;
          },
        },
        {
          accessorKey: "comment",
          header: "Comment",
          cell: ({ row }) => {
            return <div>{row.original.comment}</div>;
          },
        }
      ];
      return portfolioColumns
}