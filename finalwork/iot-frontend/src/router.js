import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/monitoring',
  },
  {
    path: '/monitoring',
    name: 'monitoring',
    component: () => import('./views/MonitoringPage.vue'),
    meta: { title: '实时监测', icon: 'monitoring' },
  },
  {
    path: '/alarms',
    name: 'alarms',
    component: () => import('./views/AlarmsPage.vue'),
    meta: { title: '报警历史', icon: 'alarms' },
  },
  {
    path: '/history',
    name: 'history',
    component: () => import('./views/HistoryPage.vue'),
    meta: { title: '历史数据', icon: 'history' },
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('./views/AboutPage.vue'),
    meta: { title: '系统设计', icon: 'about' },
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
