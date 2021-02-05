# Bubble-sheet-multiple-choice-scanner-and-test-grader
Building a bubble sheet multiple choice scanner and test grader using OMR, Python and OpenCV as an extension to <a href="https://github.com/adithi-su/Document-Scanner">https://github.com/adithi-su/Document-Scanner</a>
<br>
Steps involved - <br>
<ol>
    <li>Detect the exam in an image</li>
    <li>Apply perspective transform to extract the top-down, birds-eye-view of the exam</li>
    <li>Extract the set of bubbles(possible answer choices)</li>
    <li>Sort the questions/bubbles into rows</li>
    <li>Determine the marked amswer for each row</li>
    <li>Look-up the correct answer in the answer key</li>
    <li>Repeat for all the questions</li>
</ol>
