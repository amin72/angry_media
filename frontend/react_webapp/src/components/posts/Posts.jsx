import React, { useState } from 'react'
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
  const [posts, setPosts] = useState([
    {
      id: 1,
      owner: "admin",
      title: "Test Post x1",
      description: "Description for first project!",
      images: [
        {
          "title": "Item 1",
          "owner_description": "Image 0 is the best image ever!!!",
          "admin_description": null,
          "category": "دسته-اول",
          "image": "http://localhost:8888/image0.jpg",
          "total_views": 0
        }
      ],
      created: "2020-07-04T23:46:08.936170Z",
      updated: "2020-07-04T23:46:08.936192Z"
    },
    {
      id: 2,
      owner: "admin",
      title: "پست دوم من",
      description: "این دومین پستم هست",
      images: [
        {
          "title": "Test title from post man",
          "owner_description": null,
          "admin_description": null,
          "category": "دسته-اول",
          "image": "http://localhost:8888/image0.jpg",
          "total_views": 0
        },
        {
          "title": "پست دوم من",
          "owner_description": "asdfasdfasdf",
          "admin_description": "فضصثقضث",
          "category": "دسته-دوم",
          "image": "http://localhost:8888/image0.jpg",
          "total_views": 0
        }
      ],
      created: "2020-07-03T04:06:49.420949Z",
      updated: "2020-07-03T04:08:57.584755Z"
    },
    {
      id: 3,
      owner: "admin",
      title: "پست اول من",
      description: "این اولین پستم هست",
      images: [
        {
          "title": "پست اول امین",
          "owner_description": "پست اول امین هست. تعظیم کنید برای ایشون ;)",
          "admin_description": "",
          "category": "دسته-اول",
          "image": "http://localhost:8888/image0.jpg",
          "total_views": 0
        }
      ],
      created: "2020-07-03T02:57:33.736632Z",
      updated: "2020-07-03T04:06:38.009161Z"
    },
    {
      id: 4,
      owner: "admin",
      title: "پست اول من",
      description: "این اولین پستم هست",
      images: [
        {
          "title": "پست اول امین",
          "owner_description": "پست اول امین هست. تعظیم کنید برای ایشون ;)",
          "admin_description": "",
          "category": "دسته-اول",
          "image": "http://localhost:8888/image0.jpg",
          "total_views": 0
        }
      ],
      created: "2020-07-03T02:57:33.736632Z",
      updated: "2020-07-03T04:06:38.009161Z"
    },
    {
      id: 5,
      owner: "admin",
      title: "پست اول من",
      description: "این اولین پستم هست",
      images: [
        {
          "title": "پست اول امین",
          "owner_description": "پست اول امین هست. تعظیم کنید برای ایشون ;)",
          "admin_description": "",
          "category": "دسته-اول",
          "image": "http://localhost:8888/image0.jpg",
          "total_views": 0
        }
      ],
      created: "2020-07-03T02:57:33.736632Z",
      updated: "2020-07-03T04:06:38.009161Z"
    }
  ])
  
  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        {posts.map(post => {
          console.log(post)
          return (
            <Grid 
              key={post.id}
              item
              md={3}
              sm={4}
              xs={12}>
              <PostCard post={post} />
            </Grid>
          )
        })}
      </Grid>
    </div>
  )
}

export default Post