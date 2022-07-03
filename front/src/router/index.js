//该文件专门用于创建整个应用的路由器
import VueRouter from "vue-router";
//引入
import PageHome     from '../pages/PageHome'
import PageHub      from '../pages/PageHub'
import PageMappub   from '../pages/PageMappub'
import PageMappri   from '../pages/PageMappri'
import PageMessage  from '../pages/PageMessage'
import Login        from '../pages/Login'
import Index        from '../pages/Index'


//创建并暴露一个路由器
export default new VueRouter({
    routes: [
        {
            name: 'Index',
            path: '/',
            component: Index
        },
        {
            name: 'Login',
            path: '/login',
            component: Login
        },
        {
            name: 'PageHome',
            path: '/home',
            component: PageHome
        },
        {
            name: 'PageHub',
            path: '/hub',
            component: PageHub
        },
        {
            name: 'PageMappub',
            path: '/mappub',
            component: PageMappub
        },
        {
            name: 'PageMappri',
            path: '/mappri',
            component: PageMappri
        },
        {
            name: 'PageMessage',
            path: '/message',
            component: PageMessage,
        }
    ]
})

