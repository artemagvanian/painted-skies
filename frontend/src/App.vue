<template>
    <v-app>
        <v-navigation-drawer app right temporary v-model="drawer">
            <v-list>
                <v-list-tile :to="{name:'pdf'}">
                    <v-list-tile-action>
                        <v-icon>picture_as_pdf</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ $t("drawer.takeNotesFromPdf") }}</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <v-divider></v-divider>
                <v-list-tile :to="{name:'image'}">
                    <v-list-tile-action>
                        <v-icon>image</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ $t("drawer.takeNotesFromPicture") }}</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <v-divider></v-divider>
                <v-list-tile :to="{name:'mindmap'}">
                    <v-list-tile-action>
                        <v-icon>brush</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ $t("drawer.takeNotesFromScratch") }}</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <template v-if="Auth.checkToken()">
                    <v-divider></v-divider>
                    <v-list-tile :to="{name:'list'}">
                        <v-list-tile-action>
                            <v-icon>book</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>{{ $t("drawer.library") }}</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </template>
                <template v-else>
                    <v-divider></v-divider>
                    <v-list-tile :to="{name:'signup'}">
                        <v-list-tile-action>
                            <v-icon>arrow_upward</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>{{ $t("drawer.signUp") }}</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </template>
                <v-divider></v-divider>
                <v-list-tile :to="{name: Auth.checkToken() ? 'logout' : 'login'}">
                    <v-list-tile-action>
                        <v-icon>arrow_forward</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ Auth.checkToken() ? $t("drawer.logout") : $t("drawer.login")}}
                        </v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
        </v-navigation-drawer>
        <v-toolbar app flat prominent>
            <v-toolbar-title>Painted Skies</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn @click="$i18n.locale = 'uk'" icon>
                UK
            </v-btn>
            <v-btn @click="$i18n.locale = 'en'" icon>
                EN
            </v-btn>
            <v-btn href="//rtmk.me" icon target="_blank">
                <v-icon>info</v-icon>
            </v-btn>
            <v-btn @click="drawer = !drawer" icon>
                <v-icon>menu</v-icon>
            </v-btn>
        </v-toolbar>
        <v-content>
            <router-view></router-view>
        </v-content>
    </v-app>
</template>

<script>
    import Auth from './utils/auth'
    import axios from 'axios'
    import cookies from 'js-cookie'

    export default {
        name: 'app',
        data() {
            return {
                drawer: false,
                Auth,
            }
        },
        async mounted() {
            let csrf = await axios.get('/api/csrf');
            cookies.set('csrftoken', csrf.data.token);
        }
    }
</script>