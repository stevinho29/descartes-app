
import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { MemoryRouter } from "react-router-dom";
import PortfolioSummary from "./portfolio_summary";

jest.mock("./api/contact-api", () => ({
  getContacts: jest.fn(),
  getEmailAddresses: jest.fn()
}));

import { getContacts, getEmailAddresses } from "./api/contact-api";

const mockContacts = function(){
  (getContacts as jest.Mock).mockResolvedValue({"data":[
    { id: 1, first_name: "Steve", "last_name": "Ndemanou", "email": "ndemanousteve@gmail.com", "job": "assistant", "comment": "no comment" },
    { id: 2, first_name: "Yanis", "last_name": "dublun", "email": "yanis.dublun@gmail.com", "job": "assistant", "comment": "no comment" }
    
  ], "total": 2, "links": null, "current":1});
}

const mockEmailAddresses = function(){
  (getEmailAddresses as jest.Mock).mockResolvedValue({"data":["email1@gmail.com", "email2@gmail.com"], "total": 2, "links": null, "current":1});
}
describe("PortfolioSummary", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders a table of contacts", async () => {
    
    mockContacts()
    render(
      <MemoryRouter>
        <PortfolioSummary />
      </MemoryRouter>
    );

    await waitFor(() => {
      const rows = document.querySelectorAll('tbody tr[data-slot="table-row"]');
      expect(rows.length).toEqual(2);
    });

  });

  test("renders a list of email addresses", async () => {
    mockContacts()
    mockEmailAddresses()
    
    render(
      <MemoryRouter>
        <PortfolioSummary />
      </MemoryRouter>
    );
    await waitFor(()=>{
      const jobButton = screen.getByTestId("job-id-1");
      fireEvent.click(jobButton);
      expect(getEmailAddresses).toHaveBeenCalledTimes(1);
    })
    
    await waitFor(() => {
      const email1 = screen.getByText(/email1@gmail.com/i);
      const email2 = screen.getByText(/email2@gmail.com/i);
      expect(email1).toBeInTheDocument();
      expect(email2).toBeInTheDocument();
    })
  });
});
