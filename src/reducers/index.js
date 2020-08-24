// package imports
import { combineReducers } from 'redux'

// project imports
import authedUserReducer from './authedUser'

export default combineReducers({
  authedUser: authedUserReducer,
})