// package imports
import React from 'react'
import { connect } from 'react-redux'
import {
  Typography,
  Button
} from '@material-ui/core'

// project imports
import { testBackend } from '../util/api'

function Home({ authedUser }) {
  const [message, setMessage] = React.useState('')

  const handleTestBackend = async () => {
    testBackend()
    .then(({data}) => {
      console.log(data)
      setMessage(data.message)
    })
  }

  return (
    <div>
      {authedUser
        ? <Typography variant="h6">You are logged in, {authedUser.nickname}.</Typography>
        : <Typography variant="h6">Please login using link above.</Typography>
      }
      <Button onClick={handleTestBackend}>Click to test backend.</Button>
      <Typography variant="h6">{message}</Typography>
    </div>
  )
}

function mapStateToProps(state) {
  return {
    authedUser: state.authedUser
  }
}

export default connect(mapStateToProps)(Home)
