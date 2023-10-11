/** @type {HTMLSelectElement} */
const select = document.getElementById('select');

/** @type {HTMLDivElement} */
const otherGender = document.createElement('div');

/** @type {HTMLInputElement} */
const inputOtherGender = document.createElement('input');

/** @type {HTMLLabelElement} */
const labelOtherGender = document.createElement('label');

inputOtherGender.type = "text"
inputOtherGender.id = "gender_other"
inputOtherGender.classList.add("mt-2")
inputOtherGender.required = true
inputOtherGender.minLength = 4
inputOtherGender.maxLength = 32

labelOtherGender.classList.add("mt-2")
labelOtherGender.textContent = "Especifique como se identifica"

otherGender.classList.add("flex")
otherGender.classList.add("flex-col")

otherGender.appendChild(labelOtherGender)
otherGender.appendChild(inputOtherGender)

select.addEventListener('click', () => {
    if (select.value === "other") {
        select.parentElement.appendChild(otherGender)
    } else {
        if (select.parentElement.contains(otherGender)) {
            select.parentElement.removeChild(otherGender)
        }
    }
})