/** @type {HTMLDivElement} */
const fieldGender = document.getElementById("field_select");

/** @type {HTMLSelectElement} */
const select = document.getElementById('select');

/** @type {HTMLDivElement} */
const fieldOtherGender = document.getElementById('field_gender_other');

/** @type {HTMLInputElement} */
const inputOtherGender = document.getElementById('gender_other');

/** @type {HTMLFormElement} */
const form = select.parentElement.parentElement;
const originalFormData = new FormData(form);
const originalOtherGenderValue = originalFormData.get("gender_other") ?? "";

if (select.value !== "OTHER") {
  form.removeChild(fieldOtherGender);
}

select.addEventListener('click', () => {
  if (select.value === "OTHER") {
    fieldGender.after(fieldOtherGender);
  }
  else {
    if (form.contains(fieldOtherGender)) {
      form.removeChild(fieldOtherGender)
    }
  }
})

form.addEventListener('reset', () => {
  const originalGender = originalFormData.get("gender");
  fieldOtherGender.value = originalOtherGenderValue;

  if (originalGender !== "OTHER") {
    if (form.contains(fieldOtherGender)) {
      form.removeChild(fieldOtherGender)
    }
  }
  else {
    fieldGender.after(fieldOtherGender);
  }
});
