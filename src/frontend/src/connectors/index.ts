import { FETCH_UPLOAD_URL, FETCH_CHECK_STATUS_URL } from "../constants/endpoints";
import { getUrl } from "../helpers/navigation";

export const fetchUpload = async (formData: FormData) => {
  const task_id = new Date().getTime().toString();
  formData.append("task_id", task_id);

  try {
    const response = await fetch(FETCH_UPLOAD_URL, {
      method: "POST",
      body: formData,
    });

    const parsedResponse = await response.json();

    if (parsedResponse?.status !== "success") {
      throw new Error("Status is not success!!!");
    }

    return task_id;
  } catch (error) {
    console.error("Failed to upload file: ", error);
  }
};

export const fetchCheckStatus = async (taskId: string) => {
  const fetchUrl = getUrl(FETCH_CHECK_STATUS_URL, { taskId });
  try {
    const response = await fetch(fetchUrl);

    return response.json();
  } catch (error) {
    console.error("Failed to check status, retrying", error);
    return { status: "Pending" };
  }
};
