<script>
    import Auth from '../utils/auth'

    export default {
        name: "Logout",
        mounted() {
            Auth.destroyToken();
            this.$router.push('/')
        }
    }
</script>