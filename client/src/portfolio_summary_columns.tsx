import { ColumnDef } from "@tanstack/react-table";
import { ContactModel } from "./models/contact";
import { Edit2, Trash } from "lucide-react";
import { Button } from "./components/ui/button";

interface ColumnsProps{
  onJobClickHandler: (value:string)=>void
  onJobDeleteHandler : (value:number)=>void
  onEditJobHandler: (value:number)=>void
}
export function getPortfolioSummaryColumns({onJobClickHandler, onJobDeleteHandler, onEditJobHandler}: ColumnsProps){
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
            enableSorting: true
        },
        {
          accessorKey: "job",
          header: "Job",
          enableSorting: true,
          cell: ({ row }) => {
            return <div 
            className="font-bold cursor-pointer"
            onClick={()=>onJobClickHandler(row.original.job)}>{row.original.job}
            </div>;
          },
        },
        {
          accessorKey: "comment",
          header: "Comment",
          enableSorting: false,
          cell: ({ row }) => {
            return <div>{row.original.comment}</div>;
          },
        },
        {
          id: "actions",
          header: "Actions",
          cell: ({ row }) => {
            const contact = row.original;
            return (
              <div>
                <Button onClick={() => {
                  onJobDeleteHandler(contact.id)}}>
                <Trash className="text-red-500"></Trash>
                </Button>
                <Button onClick={() => {
                  onEditJobHandler(contact.id)}}>
                <Edit2 className="text-blue-500"></Edit2>
                </Button>
                </div>
            )
        }
      }
    ]
      
      return portfolioColumns
}