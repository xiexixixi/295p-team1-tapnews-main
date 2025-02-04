import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.min.js';
import 'bootstrap/dist/css/bootstrap.min.css';
// import NewsPanel from '../NewsPanel/NewsPanel';

// // import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//         <div className="container">
//           <NewsPanel/>
//         </div>
//     </div>
//   );
// }

// export default App;


import React from "react";
import { Switch, Route } from "react-router-dom";
import './App.css';
import NewsPanel from "../NewsPanel/NewsPanel";
import Base from "../Base/Base";
import LoginPage from "../Login/LoginPage";
import SignUpPage from "../SignUp/SignUpPage";
import NewsPanelForClass from '../NewsPanel/NewsPanelForClass';
import PersonProfile from '../Person/PersonProfile';

class App extends React.Component {
  render() {
    return (
      <div>
        <Base>
          <Switch>
            <Route path="/login" component={LoginPage} />
            <Route path="/signup" component={SignUpPage} />
            <Route path="/categories/:category" component={NewsPanelForClass} />
            <Route path="/personal" component={PersonProfile} />
            <Route path="/" component={NewsPanel} />
          </Switch>
        </Base>

      </div>
    )
  }
}
export default App;