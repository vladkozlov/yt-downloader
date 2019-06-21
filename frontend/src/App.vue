<template>
  <v-app>
    <v-toolbar app color="primary">
      <v-toolbar-title class="white--text headline text-uppercase">
        <span>YouTube</span>
        <span class="font-weight-light">Загрузчик</span>
      </v-toolbar-title>
    </v-toolbar>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      //
    }
  }
}
</script>
