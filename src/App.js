// library imports
import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'
import { connect } from 'react-redux'

// project imports
import Loading from './components/Loading'
import Nav from './components/Nav'
import { handleAutoLogin } from './actions/authedUser'
const Home = React.lazy(() => import('./components/Home'))
const Login = React.lazy(() => import('./components/Login'))
const LoginCallback = React.lazy(() => import('./components/LoginCallback'))

function App({dispatch}) {

  // check for autoLogin on initial render
  React.useEffect(() => {
    dispatch(handleAutoLogin())
  },[dispatch])

  return (
    <Router>

      <Nav />

      <React.Suspense fallback={<Loading />}>
        <Switch>
          <Route exact path='/' component={Home} />
          <Route path='/login' component={Login} />
          <Route path='/complete_login' component={LoginCallback} />
          <Route render={() => <h1>404: Not found.</h1>} />
        </Switch>
      </React.Suspense>
    </Router>
  );
}

export default connect()(App);
