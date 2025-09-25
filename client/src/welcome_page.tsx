import './welcome_page.css';

function WelcomePage() {
  return (
    <div className="WelcomePage">
      <p className="font-bold">
        Welcome !
      </p>
      <p>You can navigate to the <a href="/form" className="underline">portfolio form</a> and to the <a href="/summary" className="underline">portfolio summary</a></p>
    </div >
  );
}

export default WelcomePage;
