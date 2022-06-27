<div class="container-fluid mt-5 p-5">
    <h4 class="text-center pt-4" style="color: #CA6035;">
        <b>
            Preview Passage
        </b>
    </h4>

    <p class="mt-5">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque repellendus consequatur eveniet laborum. Rerum in perferendis labore officiis reprehenderit officia quas dolore minus, saepe repudiandae laudantium aliquam temporibus, inventore maxime? Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque repellendus consequatur eveniet laborum. Rerum in perferendis labore officiis reprehenderit officia quas dolore minus, saepe repudiandae laudantium aliquam temporibus, inventore maxime? Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque repellendus consequatur eveniet laborum. Rerum in perferendis labore officiis reprehenderit officia quas dolore minus, saepe repudiandae laudantium aliquam temporibus, inventore maxime? Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque repellendus consequatur eveniet laborum. Rerum in perferendis labore officiis reprehenderit officia quas dolore minus, saepe repudiandae laudantium aliquam temporibus, inventore maxime?
    </p>

    <div class="card mt-4">
        <div class="card-body">
            <table class="table table-borderless">
                <tr>
                    <td>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
                        </div>
                    </td>
                    <td>
                        <p>
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Perspiciatis laudantium numquam maiores nisi aut? Molestias rem, at ratione esse eius aliquid voluptatem animi. Totam tempore amet rerum fugit, sapiente rem.
                        </p>
                        <ol style="list-style-type: upper-alpha;">
                            <li>
                                Lorem
                            </li>
                            <li>
                                Ipsum
                            </li>
                            <li>
                                Dolor
                            </li>
                            <li>
                                Sit Amet
                            </li>
                        </ol>
                        <b>Ans: B</b>
                    </td>
                    <td>
                        <button type="button" class="btn" style="background-color: #3E6D81; color: white;" data-bs-toggle="modal" data-bs-target="#exampleModal">
                            <span class="iconify-inline" data-icon="akar-icons:edit" style="color: white;"></span>
                        </button>
                        <!-- Modal -->
                        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-scrollable">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="exampleModalLabel">Edit Question</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <textarea class="form-control" id="exampleFormControlTextarea1" rows="7" style="text-indent: -193px">
                                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque repellendus consequatur eveniet laborum. Rerum in perferendis labore officiis reprehenderit officia quas dolore minus, saepe repudiandae laudantium aliquam temporibus, inventore maxime? Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                                        </textarea>
                                        <textarea class="form-control mt-1" id="exampleFormControlTextarea2" rows="4" style="text-indent: -193px" html>
                                            Lorem 
                                            Ipsum 
                                            Dolor 
                                            Sit Amet
                                        </textarea>
                                        <textarea class="form-control mt-1" id="exampleFormControlTextarea3" rows="1" style="text-indent: -193px" html>
                                            B
                                        </textarea>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                        <button type="button" class="btn btn-primary">Update Question</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    <div class="card mt-4">
        <div class="card-body">
            <table class="table table-borderless">
                <tr>
                    <td>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                        </div>
                    </td>
                    <td>
                        <p>
                            Lorem ipsum dolor sit amet consectetur adipisicing elit. Perspiciatis laudantium numquam maiores nisi aut? Molestias rem, at ratione esse eius aliquid voluptatem animi. Totam tempore amet rerum fugit, sapiente rem.
                        </p>
                        <ol style="list-style-type: upper-alpha;">
                            <li>
                                Lorem
                            </li>
                            <li>
                                Ipsum
                            </li>
                            <li>
                                Dolor
                            </li>
                            <li>
                                Sit Amet
                            </li>
                        </ol>
                        <b>Ans: B</b>
                    </td>
                    <td>
                        <button class="btn" style="background-color: #3E6D81; color: white;">
                            <span class="iconify-inline" data-icon="akar-icons:edit" style="color: white;"></span>
                        </button>
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <div class="row mt-3 mb-5" style="float: right;">
        <a href="<?= base_url('generate/question_collection') ?>">
            <button class="btn" style="background-color: #3E6D81; width: 150px; color: white;">Save</button>
        </a>
    </div>
</div>