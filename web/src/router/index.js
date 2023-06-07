import Vue from 'vue'
import VueRouter from 'vue-router'
import layout from '@/layout/layout.vue'


// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'layout',
    component: layout,
    redirect: '/note',  
    children: [
      {
        path: 'note',
        name: 'note',
        component: () => import('@/views/page/note.vue'),
      },

      {
        path: 'knowledge',
        name: 'knowledge',
        component: () => import('@/views/knowledge/knowledge.vue'),
      },


    ]
  },

]

const router = new VueRouter({
  routes
})

export default router
