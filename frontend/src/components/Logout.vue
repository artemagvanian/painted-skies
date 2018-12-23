<template>

</template>

<script>
    import Auth from '../utils/auth'

    export default {
        name: "Logout",
        mounted() {
            Auth.logout(this.$session, this.$router);
        }
    }
</script>

<style scoped>

</style>