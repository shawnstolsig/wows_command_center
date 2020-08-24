// package imports
import React from 'react'
import { connect } from 'react-redux'

// project imports

function Home({authedUser}){

  return (
    <div>
      {authedUser 
      ? <h6>You are logged in, {authedUser.nickname}.</h6>
      : <h6>Please login using link above.</h6>
      }
    </div>
  )
}

function mapStateToProps(state){
  return {
    authedUser: state.authedUser
  }
}

export default connect(mapStateToProps)(Home)
