/* Javascript for XBlockControlledNavigation. */
function XBlockControlledNavigation(runtime, element) {
  const nextChild = runtime.handlerUrl(element, "next_child");
  const prevChild = runtime.handlerUrl(element, "prev_child");

  $(element)
    .find(`#prev`)
    .click(function () {
      const data = {};
      $.post(prevChild, JSON.stringify(data))
        .done(function (response) {
          window.location.reload(false);
        })
        .fail(function () {
          console.log("Error to get previous child");
        });
    });

  $(element)
    .find(`#next`)
    .click(function () {
      const data = {};
      $.post(nextChild, JSON.stringify(data))
        .done(function (response) {
          window.location.reload(false);
        })
        .fail(function () {
          console.log("Error to get next child");
        });
    });
}
