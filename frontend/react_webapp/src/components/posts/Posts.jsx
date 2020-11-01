import React from 'react'
import { makeStyles } from '@material-ui/core/styles'
import Grid from '@material-ui/core/Grid'
import PostCard from './PostCard'

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  }
}))

const Post = () => {
  const classes = useStyles()
  
  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item md={3} sm={4} xs={12}>
          <PostCard
            title="Lizard"
            imageSrc="http://localhost:8888/image0.jpg"
            description="Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging across all continents except Antarctica"
          />
        </Grid>
        <Grid item md={3} sm={4} xs={12}>
          <PostCard
            title="Lizard"
            imageSrc="http://localhost:8888/image0.jpg"
            description="Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging across all continents except Antarctica"
          />
        </Grid>
        <Grid item md={3} sm={4} xs={12}>
          <PostCard
            title="Lizard"
            imageSrc="http://localhost:8888/image0.jpg"
            description="Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging across all continents except Antarctica"
          />
        </Grid>
        <Grid item md={3} sm={4} xs={12}>
          <PostCard
            title="Lizard"
            imageSrc="http://localhost:8888/image0.jpg"
            description="Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging across all continents except Antarctica"
          />
        </Grid>
        <Grid item md={3} sm={4} xs={12}>
          <PostCard
            title="Lizard"
            imageSrc="http://localhost:8888/image0.jpg"
            description="Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging across all continents except Antarctica"
          />
        </Grid>
        <Grid item md={3} sm={4} xs={12}>
          <PostCard
            title="Lizard"
            imageSrc="http://localhost:8888/image0.jpg"
            description="Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging across all continents except Antarctica"
          />
        </Grid>
      </Grid>
    </div>
  )
}

export default Post