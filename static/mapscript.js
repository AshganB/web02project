<script type="text/javascript">
        function initMap(){
            new google.maps.Map(document.getElementById('map'),{
                center: {lat: {{location.lat}}, lng:{{location.lng}}},
                zoom:16
            });
        }
        </script>