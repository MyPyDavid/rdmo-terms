document.addEventListener("DOMContentLoaded", function () {
  var filterInput = document.getElementById("filter")
  if (!filterInput) return;

  // Collect all result cards on this page
  var elements = Array.prototype.slice.call(
    document.querySelectorAll(".element[data-uri]")
  );
  if (elements.length === 0) {
    return;
  }

  // Map url -> DOM element for quick lookup
  var elementByUri = new Map();
  elements.forEach(function (el) {
    var url = el.getAttribute("data-uri");
    if (url) {
      elementByUri.set(url, el);
    }
  });

  var miniSearch = null;
  var indexReady = false;

  // Load index.json from the same directory as this page
  fetch("index.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error("index.json not found for this page");
      }
      return response.json();
    })
    .then((data) => {
      // base fields we always want to index
      var baseFields = ["uri", "uri_path", "comment"];

      // Collect all keys starting with text_ or title_ across ALL items
      var dynamicFieldSet = new Set();

      data.forEach(function (item) {
        Object.keys(item).forEach(function (key) {
          if (/^(text_|title_)/.test(key)) {
            dynamicFieldSet.add(key);
          }
        });
      });

      var dynamicFields = Array.from(dynamicFieldSet);

      // Merge and make sure fields are unique
      var allFields = baseFields.concat(
        dynamicFields.filter(function (field) {
          return baseFields.indexOf(field) === -1;
        })
      );

      miniSearch = new MiniSearch({
        fields: allFields,
        storeFields: ["uri"],
        idField: "uri"
      });

      var docs = data
        .filter(function (item) {
          return item.uri && elementByUri.has(item.uri);
        })
        .map(function (item) {
          var doc = { uri: item.uri || "" };

          allFields.forEach(function (field) {
            // Fall back to empty string if missing / null
            doc[field] = item[field] || "";
          });

          return doc;
        });

      miniSearch.addAll(docs);
      indexReady = true;
    })
    .catch(function (err) {
      console.error("MiniSearch: could not load or build index.json", err);
    });

  function showAll() {
    elements.forEach(function (el) {
      el.classList.remove("d-none");
    });
  }

  function filterByResults(results) {
    var visibleUrls = new Set(
      results.map(function (r) {
        return r.id;
      })
    );

    elements.forEach(function (el) {
      var url = el.getAttribute("data-uri");
      if (visibleUrls.has(url)) {
        el.classList.remove("d-none");
      } else {
        el.classList.add("d-none");
      }
    });
  }

  const handleInput = (event) => {
    var query = event.target.value.trim();

    if (!indexReady || !miniSearch || !query) {
      showAll();
      return;
    }

    var options = {
      prefix: true,
      fuzzy: 0.2
    };

    // if it looks like a URL, search more strictly
    if (/^https?:\/\//.test(query)) {
      options = {
        fields: ["uri", "uri_path", "url"],
        prefix: false,
        fuzzy: false,
        combineWith: "AND"
      };
    }

    var results = miniSearch.search(query, options);

    if (results.length === 0) {
      elements.forEach(function (el) {
        el.classList.add("d-none");
      });
    } else {
      filterByResults(results);
    }
  }

  const debouncedInput = _.debounce(handleInput, 300);

  filterInput.addEventListener("input", debouncedInput);

});
