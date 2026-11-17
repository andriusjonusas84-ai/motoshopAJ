window.addEventListener("load", function() {

    const slider = document.getElementById("final_price_slider");
    if (!slider) return;

    // Read values from HTML data attributes
    const SLIDER_MIN = parseInt(slider.dataset.min);
    const SLIDER_MAX = parseInt(slider.dataset.max);
    const START_MIN = parseInt(slider.dataset.startMin);
    const START_MAX = parseInt(slider.dataset.startMax);

    // Žingsnis pagal kainų intervalą
    const range = SLIDER_MAX - SLIDER_MIN;
    let STEP = 50;
    if (range <= 200) {
        STEP = 1;
    } else if (range <= 2000) {
        STEP = 10;
    }

    noUiSlider.create(slider, {
        start: [START_MIN, START_MAX],
        connect: true,
        step: STEP,
        range: {
            min: SLIDER_MIN,
            max: SLIDER_MAX
        }
    });

    // Įrašo kainas į abu matomus laukelius ir į paslėptus formos laukus
    function setPriceInputs(min, max) {
        document.getElementById("id_final_price_0").value = min;
        document.getElementById("id_final_price_1").value = max;
        document.getElementById("final_price_value_min").value = min;
        document.getElementById("final_price_value_max").value = max;
    }

    // Tempiant slankiklį – reikšmės pagal žingsnį
    slider.noUiSlider.on('update', function(values) {
        setPriceInputs(Math.round(values[0]), Math.round(values[1]));
    });

    // Atkuriam tikslias reikšmes (ne suapvalintas pagal žingsnį)
    setPriceInputs(START_MIN, START_MAX);

    // Paleidus rankenėlę – filtruoti iškart
    slider.noUiSlider.on('change', function () {
        document.getElementById('product-filter-form').requestSubmit();
    });

    // Įvedus kainą ranka – paliekam tikslią reikšmę
    document.getElementById("final_price_value_min").addEventListener("change", function() {
        let min = parseInt(this.value) || SLIDER_MIN;
        let max = parseInt(document.getElementById("final_price_value_max").value) || SLIDER_MAX;

        min = Math.max(SLIDER_MIN, Math.min(min, max));
        slider.noUiSlider.set([min, max]);
        setPriceInputs(min, max);
    });

    document.getElementById("final_price_value_max").addEventListener("change", function() {
        let min = parseInt(document.getElementById("final_price_value_min").value) || SLIDER_MIN;
        let max = parseInt(this.value) || SLIDER_MAX;

        max = Math.min(SLIDER_MAX, Math.max(max, min));
        slider.noUiSlider.set([min, max]);
        setPriceInputs(min, max);
    });

    document.getElementById("product-filter-form").addEventListener("submit", function() {
        const min = parseInt(document.getElementById("id_final_price_0").value);
        const max = parseInt(document.getElementById("id_final_price_1").value);

        if (min === SLIDER_MIN && max === SLIDER_MAX) {
            document.getElementById("id_final_price_0").value = "";
            document.getElementById("id_final_price_1").value = "";
        }
    });
});