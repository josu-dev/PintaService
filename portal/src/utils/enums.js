/**
 * @type {{
 *  MALE: 'Masculino',
 *  FEMALE: 'Femenino',
 *  OTHER: 'Otros(Por favor especifica)',
 *  NOT_SPECIFIED: 'Prefiero no decir'
 * }}
 */
export const genderOptions = {
  MALE: 'Masculino',
  FEMALE: 'Femenino',
  OTHER: 'Otros(Por favor especifica)',
  NOT_SPECIFIED: 'Prefiero no decir'
};
/**
 * @typedef {typeof genderOptions[keyof typeof genderOptions]} GenderOptions
 */

/**
 * @type {{
 *  DNI: 'DNI',
 *  LC: 'Libreta Civica',
 *  LE: 'Libreta de Enrolamiento'
 * }}
 */
export const documentTypes = {
  DNI: 'DNI',
  LC: 'Libreta Civica',
  LE: 'Libreta de Enrolamiento'
};
/**
 * @typedef {typeof documentTypes[keyof typeof documentTypes]} DocumentTypes
 */

/**
 * @type {{
 *  ANALYSIS: 'analisis',
 *  CONSULTANCY: 'consultoria',
 *  DEVELOPMENT: 'desarrollo'
 * }}
 */
export const serviceTypes = {
  ANALYSIS: 'analisis',
  CONSULTANCY: 'consultoria',
  DEVELOPMENT: 'desarrollo'
};
/**
 * @typedef {typeof serviceTypes[keyof typeof serviceTypes]} ServiceTypes
 */

/**
 * @type {{
 *  ACCEPTED: 'Aceptada',
 *  REJECTED: 'Rechazada',
 *  IN_PROCESS: 'En Proceso',
 *  FINISHED: 'Finalizada',
 *  CANCELED: 'Cancelada'
 * }}
 */
export const requestStatus = {
  ACCEPTED: 'Aceptada',
  REJECTED: 'Rechazada',
  IN_PROCESS: 'En Proceso',
  FINISHED: 'Finalizada',
  CANCELED: 'Cancelada'
};
/**
 * @typedef {typeof requestStatus[keyof typeof requestStatus]} RequestStatus
 */
