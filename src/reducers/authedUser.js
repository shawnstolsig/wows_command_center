import { LOGIN_USER, LOGOUT_USER } from '../actions/authedUser'

export default function authReducer(state = null, action) {
  switch (action.type) {

    case LOGIN_USER:
      return {
        ...action.authedUser
      }

    case LOGOUT_USER:
      return null

    default:
      return state

  }
}