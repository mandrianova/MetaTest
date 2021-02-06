<template>
  <b-container class="mx-0 px-0">
    <div v-if="loading" class="d-flex justify-content-center">
      <Loader class="my-5" />
    </div>
    <b-alert v-if="message" v-bind:variant="message_type" show="" class="my-5">
      {{message}}
    </b-alert>
    <b-container>
    <b-card class="my-5">
      <b-row no-gutters>
        <b-col md="4" class="overflow-hidden d-flex justify-content-center">
          <b-card-img :src="imgUrl" :alt="name" center class="img-responsive w-auto" height="512px"/>
        </b-col>
        <b-col md="8">
          <b-card-body>
            <h1 class="mb-3">{{name}}</h1>
            <h5 v-if="methods">Методы:</h5>
            <h5><b-badge pill variant="info" v-for="(method, key) in methods" :key="key" class="mr-2">{{method}}</b-badge></h5>
          </b-card-body>
        </b-col>
      </b-row>
    </b-card>

    </b-container>
  </b-container>
</template>

<script>
import MetaResource from '@/services/Meta'
import image from '../img/freud.jpg'
import Loader from '@/components/Loader'
const service = new MetaResource()
export default {
  props: ['id'],
  components: {
    Loader
  },
  data () {
    return {
      name: '',
      imgUrl: '',
      methods: [],
      message: '',
      loading: true,
      message_type: 'danger'
    }
  },
  mounted () {
    service.getDoctor(this.id)
      .then(json => {
        this.name = json.name
        this.imgUrl = json.photo && json.photo.large_source_url ? json.photo.large_source_url : image
        this.methods = json.methods
        this.loading = false
      }).catch(() => {
        this.message = 'Ошибка на сервере'
        this.message_type = 'danger'
        this.loading = false
      })
  }
}
</script>
