import Vue from 'vue'
import Router from 'vue-router'


import bookList from '../page/library-manage/bookList.vue'

import authorList from '../page/author-manage/authorList.vue'

import publishList from '../page/publish-manage/publishList.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/bookList',
      name: 'bookList',
      component: bookList
    },
    {
      path: '/authorList',
      name: 'authorList',
      component: authorList
    },
    {
      path: '/publishList',
      name: 'publishList',
      component: publishList
    },
    {path:'*',component:bookList}
  ]
})
