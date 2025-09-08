// script.js
// 5) Closure to track successful submissions
const createSubmissionCounter = () => {
  let count = 0;
  return () => {
    count += 1;
    console.log(`Successful submissions: ${count}`);
  };
};
const incrementSubmissionCount = createSubmissionCounter();

// 1) Arrow function validator
const validateForm = (form) => {
  const content = form.querySelector('[name="content"]').value.trim();
  const termsChecked = form.querySelector('#terms').checked;

  // 1a) Content length > 25
  if (content.length <= 25) {
    alert('Blog content should be more than 25 characters');
    return false;
  }

  // 1b) Terms checkbox checked
  if (!termsChecked) {
    alert('You must agree to the terms and conditions');
    return false;
  }

  return true;
};

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Run validation
    if (!validateForm(form)) return;

    // 2) Convert form data to JSON and log
    const formDataObj = {
      // map to "title" for the destructuring step later
      title: form.querySelector('[name="blogTitle"]').value.trim(),
      author: form.querySelector('[name="authorName"]').value.trim(),
      email: form.querySelector('[name="email"]').value.trim(),
      content: form.querySelector('[name="content"]').value.trim(),
      category: form.querySelector('[name="category"]').value
    };

    const jsonString = JSON.stringify(formDataObj);
    console.log('JSON string:', jsonString);

    // 3) Parse, destructure title & email, and log
    const parsed = JSON.parse(jsonString);
    const { title, email } = parsed;
    console.log('Title:', title);
    console.log('Email:', email);

    // 4) Spread operator to add submissionDate; log updated object
    const updated = { ...parsed, submissionDate: new Date().toISOString() };
    console.log('Updated object with submissionDate:', updated);

    // 5) Count successful submissions (via closure)
    incrementSubmissionCount();
  });
});
