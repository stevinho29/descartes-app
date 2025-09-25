import { useCallback, useEffect, useState } from 'react';
import './portfolio_summary.css';
import { PaginationState, SortingState, Updater } from '@tanstack/react-table';
import { ContactModel } from './models/contact';
import { getDatatablePageInfo, getDatatableSortingState, getRange, getSortAndDesc } from './lib/datatables';
import { deleteContact, getContacts, getEmailAddresses } from './api/contact-api';
import { getPortfolioSummaryColumns } from './portfolio_summary_columns';
import { SpinnerWrapper } from './components/ui/spinner';
import { DataTable } from './components/common/datatable';
import React from 'react';
import { useNavigate } from 'react-router-dom';

function PortfolioSummary() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [emailAddresses, setEmailAddresses] = useState<string[]>([])
  const [job, setJob] = useState<string | undefined>(undefined)
  const [params, setParams] = useState({
    range: "0-10",
    sort: ["first_name"],
    desc: ["last_name"]
  })

  const [result, setResult] = useState<{
    contacts: ContactModel[];
    rowCount: number;
    pagination: PaginationState;
    sorting: SortingState;
  }>({
    contacts: [],
    rowCount: 0,
    pagination: {
      pageIndex: 0,
      pageSize: 10
    },
    sorting: []
  })

  const fetchContacts = useCallback(() => {
    setIsLoading(true)
    getContacts(params).then((res) => {

      const result = res.data as ContactModel[]
      const total = res.total ?? 0
      const datatableInfo = getDatatablePageInfo(params.range, total);
      const sortingState = getDatatableSortingState(params.sort, params.desc);

      setResult({
        contacts: result,
        rowCount: total,
        pagination: {
          pageIndex: datatableInfo.currentPage,
          pageSize: datatableInfo.sizePerPage,
        },
        sorting: sortingState,
      });

    }).catch(err => console.log(err)).finally(() => setIsLoading(false))
  }, [params]);

  useEffect(() => {
    fetchContacts()
  }, [fetchContacts])



  const handlePaginationChange = function (updater: Updater<PaginationState>) {
    const data = typeof updater === 'function' ? updater(result.pagination) : updater;
    const range = getRange(data.pageIndex, data.pageSize)
    setParams((prev) => ({ ...prev, range }))
  }

  const handleSortingChange = function (updater: Updater<SortingState>) {
    const nextSorting =
      typeof updater === 'function' ? updater(result.sorting) : updater;
    const { sort, desc } = getSortAndDesc(nextSorting)
    setParams((prev) => ({ ...prev, sort, desc }))
  }

  const onEditJobHandler = function(jobId:number){
    navigate(`/form/${jobId}`)
  }
  const onJobClickHandler = function (job: string) {

    getEmailAddresses({ job: job, only: ["email"] }).then(res => {
      let emails = res.data as string[]
      setJob(job)
      setEmailAddresses(emails)
    })
  }
  const onJobDeleteHandler = function (jobId: number) {
    deleteContact(jobId).then(res => {
      fetchContacts()
    }).catch(err => console.log(err))
  }
  const portfolioColumns = getPortfolioSummaryColumns({ onJobClickHandler, onJobDeleteHandler, onEditJobHandler })
  return (
    <div className="PortfolioSummary">
      <h1 className='font-bold text-3xl'>
        Welcome to the portfolio summary
      </h1>
      <p><a href="/" className="underline">Take me back home!</a></p>
      <div className="m-4 p-10">
        <SpinnerWrapper isLoading={isLoading}>
          <DataTable columns={portfolioColumns}
            data={result.contacts}
            rowCount={result.rowCount}
            pagination={result.pagination}
            onPaginationChange={handlePaginationChange}
            sorting={result.sorting}
            OnSortingChange={handleSortingChange} />
        </SpinnerWrapper>
      </div>

      {job && emailAddresses &&
        <React.Fragment>
          <h1> Email adresses for job: {job}</h1>
          <ul>
            {emailAddresses.map((email, index) => {
              return (
                <li key={index}>{email}</li>
              )
            })}
          </ul>
        </React.Fragment>
      }
    </div>
  );
}

export default PortfolioSummary;