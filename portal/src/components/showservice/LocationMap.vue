<script>
  import pointer from '@/assets/map-pin.svg';
  import Feature from 'ol/Feature';
  import Map from 'ol/Map';
  import View from 'ol/View';
  import Point from 'ol/geom/Point';
  import TileLayer from 'ol/layer/Tile';
  import VectorLayer from 'ol/layer/Vector';
  import { fromLonLat } from 'ol/proj';
  import OSM from 'ol/source/OSM';
  import VectorSource from 'ol/source/Vector';
  import { Icon, Style } from 'ol/style';

  export default {
    name: 'MapComponent',
    data() {
      return {
        map: null
      };
    },
    props: {
      location: {
        type: String,
        required: true
      }
    },
    mounted() {
      const [latitude, longitude] = this.location.split(',');

      const lat = Number(latitude);
      const lon = Number(longitude);

      // @ts-ignore
      this.map = new Map({
        // @ts-ignore
        target: this.$refs.mapContainer,
        layers: [
          new TileLayer({
            source: new OSM()
          })
        ],
        view: new View({
          center: fromLonLat([lon, lat]),
          zoom: 10
        })
      });

      let marker = new Feature({
        geometry: new Point(fromLonLat([lon, lat]))
      });

      let markerStyle = new Style({
        image: new Icon({
          anchor: [0.5, 1],
          src: pointer
        })
      });

      marker.setStyle(markerStyle);

      let vectorLayer = new VectorLayer({
        source: new VectorSource({
          features: [marker]
        })
      });

      // @ts-ignore
      this.map.addLayer(vectorLayer);
    }
  };
</script>

<style scoped>
  #map {
    width: 100%;
    height: 400px;
  }
</style>

<template>
  <h1 class="text-4xl font-bold text-center text-primary mb-4">¿Cómo Llegar?</h1>
  <div id="map" ref="mapContainer"></div>
</template>
