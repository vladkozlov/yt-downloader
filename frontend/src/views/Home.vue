<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center text-xs-center wrap>
      <v-flex xs12 md8 lg6>
          <v-form 
            ref="form"
            v-model="ytFormValid"
            lazy-validation
          >
            <v-text-field
              v-model="link"
              :placeholder="$t('textfield.linkFieldPlaceholder') "
              :rules="[v => isValid(v) || $t('textfield.linkFieldValidRule')]"
              required
              solo
            ></v-text-field>
            <v-btn color="primary" :loading="buttonLoading" @click="download">{{ $t('button.download') }} <v-icon right dark>cloud_download</v-icon></v-btn>
          </v-form>

          <v-card v-if="youtubeData">
            <v-container text-xs-left>
                <v-layout column>
                    <span><span class="font-weight-medium">{{ $t('video.title') }}:</span> {{youtubeData.title}}</span>
                    <span><span class="font-weight-medium">{{ $t('video.rating') }}:</span> {{youtubeData.rating}}</span>
                    <span><span class="font-weight-medium">{{ $t('video.views') }}:</span> {{youtubeData.views}}</span>

                  <template v-for="(stream ,i) in youtubeData.streams">
                    <v-btn :key="i" color="primary" @click="doStreamDownload(stream)">{{buttonNameGenerator(stream)}}</v-btn>  
                  </template>

                </v-layout>
            </v-container>
          </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
const ytLinkRegExp = /^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$/gi;

export default {
  props:{
    text: {
      type: String,
      default: ""
    }
  },
  data: () => ({
    link: "",
    ytFormValid: true,
    youtubeData: null,
    buttonLoading: false
  }),
  methods: {
    isValid(ytLink) {
      return ytLink.match(ytLinkRegExp) != null;
    },
    download() {
      if (this.$refs.form.validate()) {
        this.youtubeData = null;
        console.log(this.link);
        let postQuery = {
          link: this.link
        };

        this.buttonLoading = true
        axios
          .get(`/api/getlinks?link=${this.link}`)
          .then((data) => {
            this.buttonLoading = false;
            console.log(data);
            this.youtubeData = data.data;
          })
          .catch((e) => {
            this.buttonLoading = false;
            console.error(e)
          }) 
      }
    },
    buttonNameGenerator(stream) {
      let name = ''
      let format = stream.mimeType.split('/')[1];
      switch (stream.resolution) {
        case '1080p':
        case '720p':
            name += this.$t('quality.high')
          break;
        default:
          name += this.$t('quality.low')
          break;
      }
      name += ` (${format})`
      return name
    },
    doStreamDownload(stream) {
      window.location.assign(stream.url);
    }
  },
  mounted() {
    if (this.text) {
      this.link = this.text;
    }
  }
}
</script>
