// package imports
import React from 'react'
import queryStrings from 'query-string'
import { Redirect } from 'react-router-dom'
import { connect } from 'react-redux'

// project imports
import { handleLoginUser } from '../actions/authedUser'

function LoginCallback({ dispatch, location }) {

  // get the user's information as it's returned from WG's OpenID
  const params = queryStrings.parse(location.search)

  // if user is not logged in and we got an access token back from WG, then login user to store
  React.useEffect(() => {
    if (params.accountID) {
      dispatch(handleLoginUser(params))
    }
  }, [dispatch, params])

  // redirect user to home page if successful, or back to login if unsuccessful
  return (
    <React.Fragment>
      {params.accountID ? <Redirect to="/" /> : <Redirect to="/login?error=1" /> }
    </React.Fragment>
    
  )

}

export default connect()(LoginCallback)