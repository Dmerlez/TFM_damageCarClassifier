export const HOST = "http://localhost:8000";

const UPLOAD = "/upload";
const CHECK_STATUS = "/check-status/:taskId";
const CONFIRM = "/confirm/:taskId";

export const FETCH_UPLOAD_URL = HOST + UPLOAD;
export const FETCH_CHECK_STATUS_URL = HOST + CHECK_STATUS;
export const FETCH_CONFIRM_URL = HOST + CONFIRM;
