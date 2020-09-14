// project imports
import { verifyToken, getNewTokens } from '../util/api'

// export action types
export const LOGIN_USER = 'LOGIN_USER'
export const LOGOUT_USER = 'LOGOUT_USER'

// ACTION CREATORS
function actionLoginUser(authedUser) {
  return {
    type: LOGIN_USER,
    authedUser
  }
}

function actionLogoutUser() {
  return {
    type: LOGOUT_USER
  }
}
// END ACTION CREATORS

export function handleLoginUser(allUserDetails) {
  return (dispatch) => {

    // set user in store
    dispatch(actionLoginUser(allUserDetails))

    // store user info in localstorage for auto login.  can't store object in localstorage so must stringify
    localStorage.setItem('authedUser', JSON.stringify(allUserDetails))

  }
}

export function handleLogoutUser() {
  return (dispatch) => {
    // clear store
    dispatch(actionLogoutUser())
    // clear local storage
    localStorage.removeItem('authedUser')
  }
}

export function handleAutoLogin() {
  return async (dispatch) => {

    // check to see if authedUser info exists
    let authedUser = JSON.parse(localStorage.getItem('authedUser'))

    if (authedUser) {

      // check to see if refresh token is valid
      verifyToken(authedUser.refresh)
      // if valid refresh token...
      .then(() => {
        
        console.log(`Refresh token is valid`)

        // ....obtain new token pair, with validated refresh token
        return getNewTokens(authedUser.refresh)
        
      })
      // if successfully got new access token...
      .then((res) => {
        console.log("Successfully obtained new access token: ", res.data)

        // ...update authedUser with new access token
        authedUser.access = res.data.access

        // dispatch Login action with updated access token
        dispatch(actionLoginUser(authedUser))
        console.log("Autologin successful!")
      })
      // if any issues with tokens....
      .catch((err) => {
        console.log(`Autologin failed: refresh token no longer valid.`)
        // ....clear the previous authed user info from the browser
        localStorage.removeItem('authedUser')
      })
    }
    else {
      console.log("Autologin failed: no user info found in local storage.")
    }
  }
}