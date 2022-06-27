<div class="container-fluid mt-5 p-5">
    <h4 class="text-center pt-4" style="color: #CA6035;">
        <b>
            Generate Error Identification Question
        </b>
    </h4>

    <p class="pt-5">
        Error identification, consisting of sentences which contain four expressions, single words or two or three words underlined phrases. The test-taker's job is to identify the right phrases. all errors involve grammar or punctuation and spelling.
    </p>

    <form action="" method="POST">
        <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label"><b>Input Method</b></label><br>
            <select class="form-select" aria-label="Default select example" onchange="showDiv(this)">
                <option value="0">File TXT</option>
                <option value="1">Link</option>
            </select>
        </div>
        <div id="form-link" style="display:block;">
            <label class="form-label"><b>File TXT</b></label>
            <div class="mb-3">
                <input class="form-control" type="file" id="formFile">
            </div>
        </div>
        <div id="form-txt" style="display:none;">
            <label class="form-label"><b>Link</b></label>
            <div class="mb-3">
                <input class="form-control" type="text" placeholder="Input Link URL" aria-label="default input example">
            </div>
        </div>
    </form>

    <div class="row mt-3" style="float: right;">
        <a href="<?= base_url('generate/preview_passage') ?>">
            <button class="btn" style="background-color: #3E6D81; width: 150px; color: white;">Generate</button>
        </a>
    </div>
</div>

<script type="text/javascript">
    function showDiv(select) {
        if (select.value == 0) {
            document.getElementById('form-link').style.display = "block";
            document.getElementById('form-txt').style.display = "none";
        } else {
            document.getElementById('form-link').style.display = "none";
            document.getElementById('form-txt').style.display = "block";
        }
    }
</script>