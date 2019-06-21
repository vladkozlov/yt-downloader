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
              label="Ссылка на YouTube видео"
              placeholder="Вставьте ссылку на YouTube видео"
              :rules="[v => isValid(v) || 'Введите корректную ссылку']"
              required
              solo
            ></v-text-field>
            <v-btn color="primary" :loading="buttonLoading" @click="download">Скачать <v-icon right dark>cloud_download</v-icon></v-btn>
            <v-card v-if="url || title || text">
              <h1>Parameters</h1>
              {{title}}
              {{text}}
              {{url}}
            </v-card>
          </v-form>

          <v-card v-if="youtubeData">
            <v-container text-xs-left>
                <v-layout column>
                  <v-flex xs12>
                    <span class="font-weight-medium">Название:</span>
                    {{youtubeData.title}}
                  </v-flex>

                  <template v-for="(stream ,i) in youtubeData.streams">
                    <v-btn :key="i" color="primary" @click="doStreamDownload(stream)">{{buttonNameGenerator(stream)}}</v-btn>  
                  </template>


                  <v-flex xs12>
                    <span class="font-weight-medium">Рейтинг:</span> 
                    {{youtubeData.rating}}
                    <span class="font-weight-medium">Просмотров:</span> {{youtubeData.views}}
                  </v-flex>

                  <span class="font-weight-medium">Описание:</span> 
                  {{youtubeData.description}}
                  
                </v-layout>
            </v-container>
          </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
const testLink = "https://www.youtube.com/watch?v=jKv_N0IDS2A";
const ytLinkRegExp = /^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$/gi;

export default {
  props:{
    url: {
      type: String,
      default: ""
    },
    text: {
      type: String,
      default: ""
    },
    title: {
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
          .get(`http://localhost:8081/getlinks?link=${this.link}`)
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
            name += 'Высокое качестве'
          break;
        default:
          name += 'Низкое качество'
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
    console.log({
      url: this.url,
      text : this.text,
      title: this.title
    })
    if (this.url) {
      this.link = this.url;
    }
  }
}
</script>
