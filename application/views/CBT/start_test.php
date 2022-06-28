<div class="container-fluid p-5 mt-5">
    <p id="demo" class="mt-2" style="color: #3E6D81; font-size: 20px; font-weight: 600; text-align: right;"></p>
    <div class="mb-4 mt-5">
        <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque repellendus consequatur eveniet laborum. Rerum in perferendis labore officiis reprehenderit officia quas dolore minus, saepe repudiandae laudantium aliquam temporibus, inventore maxime? Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque repellendus consequatur eveniet laborum. Rerum in perferendis labore officiis reprehenderit officia quas dolore minus, saepe repudiandae laudantium aliquam temporibus, inventore maxime? Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque repellendus consequatur eveniet laborum. Rerum in perferendis labore officiis reprehenderit officia quas dolore minus, saepe repudiandae laudantium aliquam temporibus, inventore maxime? Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque repellendus consequatur eveniet laborum. Rerum in perferendis labore officiis reprehenderit officia quas dolore minus, saepe repudiandae laudantium aliquam temporibus, inventore maxime?
        </p>
    </div>

    <p>
        1. Lorem ipsum dolor sit amet consectetur adipisicing elit. Perspiciatis laudantium numquam maiores nisi aut? Molestias rem, at ratione esse eius aliquid voluptatem animi. Totam tempore amet rerum fugit, sapiente rem.
    </p>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
        <label class="form-check-label" for="flexRadioDefault1">
            Lorem
        </label>
    </div>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
        <label class="form-check-label" for="flexRadioDefault1">
            Ipsum
        </label>
    </div>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
        <label class="form-check-label" for="flexRadioDefault1">
            Dolor
        </label>
    </div>
    <div class="form-check">
        <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
        <label class="form-check-label" for="flexRadioDefault1">
            Sit Amet
        </label>
    </div>

    <div class="row mt-3" style="float: right;">
        <a href="<?= base_url('CBT/result_test') ?>">
            <button class="btn" style="background-color: #3E6D81; width: 150px; color: white;">Submit</button>
        </a>
    </div>
</div>

<script>
    // Set the date we're counting down to
    var countDownDate = new Date("Jun 28, 2022 13:00:00").getTime();

    // Update the count down every 1 second
    var x = setInterval(function() {

        // Get today's date and time
        var now = new Date().getTime();

        // Find the distance between now and the count down date
        var distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Output the result in an element with id="demo"
        document.getElementById("demo").innerHTML = "<span class='iconify-inline' data-icon='fluent:timer-12-regular' style='color: #3e6d81;'></span>   " + hours + "h " +
            minutes + "m " + seconds + "s ";

        // If the count down is over, write some text 
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("demo").innerHTML = "EXPIRED";
        }
    }, 1000);
</script>