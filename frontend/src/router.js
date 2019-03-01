import Vue from "vue";
import VueRouter from "vue-router";
import MindmapViewer from './components/MindmapViewer'
import PdfUploader from './components/PdfUploader'
import ImageUploader from './components/ImageUploader'
import CanvasSelector from './components/CanvasSelector'
import Menu from './components/Menu'
import MindmapList from './components/MindmapList'
import Login from './components/Login'
import Logout from './components/Logout'
import Signup from './components/Signup'

Vue.use(VueRouter);

const routes = [
    {path: '/mindmap-viewer', component: MindmapViewer, props: true, name: 'mindmap'},
    {path: '/canvas-selector', component: CanvasSelector, props: true, name: 'canvas'},
    {path: '/', component: Menu, name: 'menu'},
    {path: '/pdf-uploader', component: PdfUploader, name: 'pdf'},
    {path: '/image-uploader', component: ImageUploader, name: 'image'},
    {path: '/list', component: MindmapList, name: 'list'},
    {path: '/login', component: Login, name: 'login'},
    {path: '/logout', component: Logout, name: 'logout'},
    {path: '/signup', component: Signup, name: 'signup'},
];

const router = new VueRouter({
    routes
});

export default router
