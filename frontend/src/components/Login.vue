<template>
    <v-container fill-height fluid>
        <v-layout align-center justify-center>
            <v-flex md4 sm8 xs12>
                <v-card class="elevation-12">
                    <v-toolbar color="primary" dark>
                        <v-toolbar-title>{{ $t("auth.loginTitle") }}</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form @submit="onSubmit">
                            <v-text-field :error-messages="errors.username" :label="$t('auth.username')" id="username"
                                          name="username" prepend-icon="person" type="text"
                                          v-model="username"></v-text-field>
                            <v-text-field :error-messages="errors.password" :label="$t('auth.password')" id="password"
                                          name="password" prepend-icon="lock" type="password"
                                          v-model="password"></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn @click="onSubmit" color="primary">{{ $t("auth.login") }}</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import Auth from '../utils/auth'

    export default {
        name: "Login",
        data() {
            return {
                username: "",
                password: "",
                errors: [],
            }
        },
        methods: {
            async onSubmit() {
                try {
                    const response = await Auth.obtainToken(this.username, this.password);
                    Auth.saveToken(response.data.access);
                    this.$router.push('/')
                } catch (e) {
                    this.errors = e.response.data;
                }
            }
        }
    }
</script>