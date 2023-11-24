<script>
  import pointer from '@/assets/map-pin.svg';
  import { useToastStore } from '@/stores/toast';
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

  const toastStore = useToastStore();

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
      },
      contact: {
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
      // Add this after defining the marker
      // @ts-ignore

      // @ts-ignore
      this.map.addLayer(vectorLayer);
      // @ts-ignore
      this.map.on('click', (e) => {
        // @ts-ignore
        let features = this.map.getFeaturesAtPixel(e.pixel);
        if (features.length > 0) {
          toastStore.success('Contactanos!  ' + this.contact, { timeout: 5000 });
        }
      });
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
  <h2 class="text-xl md:text-2xl font-bold text-center mb-2 mt-4">Como Llegar</h2>
  <div id="map" ref="mapContainer"></div>
</template>
