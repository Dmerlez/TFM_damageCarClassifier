export const getUrl = (urlRoute: string, pathParams?: Record<string, string>, queryParams?: Record<string, string>) => {
  let url = urlRoute;

  if (typeof pathParams === "object") {
    Object.entries(pathParams).forEach(([key, value]) => {
      url = url.replace(`:${key}`, value);
    });
  }

  if (typeof queryParams === "object") {
    url = `${url}?${new URLSearchParams(queryParams)}`;
  }

  return url;
};
