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

    // pull out only the user info we want to save
    const { access_token, account_id, expires_at, nickname } = allUserDetails
    const authedUser = {
      accessToken: access_token,
      accountID: account_id,
      expiresAt: expires_at,
      nickname,
    }

    // set user in store
    dispatch(actionLoginUser(authedUser))

    // store user info in localstorage for auto login.  can't store object in localstorage so must stringify
    localStorage.setItem('authedUser', JSON.stringify(authedUser))

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
  return (dispatch) => {

    // check to see if authedUser info exists
    let authedUser = JSON.parse(localStorage.getItem('authedUser'))
    if (authedUser) {
      // if so, check to see if it hasn't expired (or wont't within the buffer time)
      const bufferTimeInMin = 30
      if (authedUser.expiresAt - Date.now() / 1000 > bufferTimeInMin * 60) {
        // refresh token?
        // store authedUser info in state
        dispatch(actionLoginUser(authedUser))
        console.log("Autologin successful!")
      }
      // if it has expired, clear localstorage
      else {
        console.log("Autologin failed: User's token has expired.")
        localStorage.removeItem('authedUser')
      }
    }
    else {
      console.log("Autologin failed: No user info found in local storage.")
    }
  }
}