// library imports
import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'
import { connect } from 'react-redux'
import {
  Container
} from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'

// project imports
import Loading from './components/Loading'
import Nav from './components/Nav'
import { handleAutoLogin } from './actions/authedUser'
const Home = React.lazy(() => import('./components/Home'))
const Login = React.lazy(() => import('./components/Login'))
const LoginCallback = React.lazy(() => import('./components/LoginCallback'))

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  // necessary for content to be below app bar
  toolbar: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
}))

function App({ dispatch }) {

  const classes = useStyles()

  // check for autoLogin on initial render
  React.useEffect(() => {
    dispatch(handleAutoLogin())
  }, [dispatch])

  return (
    <Router>

      <Nav />
      <div className={classes.toolbar} />

      {/* <Container> */}
        <React.Suspense fallback={<Loading />}>
          <Switch>
            <Route exact path='/' component={Home} />
            <Route path='/login' component={Login} />
            <Route path='/complete_login' component={LoginCallback} />
            <Route render={() => <h1>404: Not found.</h1>} />
          </Switch>
        </React.Suspense>
      {/* </Container> */}


    </Router>
  );
}

export default connect()(App);
