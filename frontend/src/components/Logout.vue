<script>
    export default {
        name: "Logout",
        mounted() {
            this.$session.destroy();
            this.$router.push('/');
        }
    }
</script>