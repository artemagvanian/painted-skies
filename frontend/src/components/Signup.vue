<template>
    <v-container fill-height fluid>
        <v-layout align-center justify-center>
            <v-flex md4 sm8 xs12>
                <v-card class="elevation-12">
                    <v-toolbar color="primary" dark>
                        <v-toolbar-title>{{ $t('auth.signUpTitle') }}</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-form>
                            <v-text-field :error-messages="errors.username" :label="$t('auth.username')" name="login"
                                          prepend-icon="person" type="text" v-model="username"></v-text-field>
                            <v-text-field :error-messages="errors.password1" :label="$t('auth.password')" id="password1"
                                          name="password1" prepend-icon="lock" type="password"
                                          v-model="password1"></v-text-field>
                            <v-text-field :error-messages="errors.password2" :label="$t('auth.repeatPassword')"
                                          id="password2" name="password2" prepend-icon="lock" type="password"
                                          v-model="password2"></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn @click="onSubmit" color="primary">{{ $t('auth.signUp') }}</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import Auth from '../utils/auth'

    export default {
        name: "Signup",
        data() {
            return {
                username: "",
                password1: "",
                password2: "",
                errors: [],
            }
        },
        methods: {
            async onSubmit() {
                try {
                    await Auth.signup(this.username, this.password1, this.password2);
                    this.$router.push('/');
                } catch (e) {
                    this.errors = e.response.data;
                }
            }
        }
    }
</script>