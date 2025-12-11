document.addEventListener("DOMContentLoaded", function () {
  var searchInput = document.getElementById("search");
  if (!searchInput) return;

  if (typeof MiniSearch === "undefined") {
    console.error("MiniSearch not found. Check minisearch.min.js script tag.");
    return;
  }

  // Collect all result cards on this page
  var elements = Array.prototype.slice.call(
    document.querySelectorAll(".element[data-url]")
  );
  if (elements.length === 0) {
    return;
  }

  // Map url -> DOM element for quick lookup
  var elementByUrl = new Map();
  elements.forEach(function (el) {
    var url = el.getAttribute("data-url");
    if (url) {
      elementByUrl.set(url, el);
    }
  });

  var miniSearch = null;
  var indexReady = false;

  // Load index.json from the same directory as this page
  fetch("index.json")
    .then(function (res) {
      if (!res.ok) {
        throw new Error("index.json not found for this page");
      }
      return res.json();
    })
    .then(function (data) {
      if (!data || !data.length) {
        return;
      }

      // --- CENTRALIZE / AUTO-DETECT FIELDS ------------------------

      // base fields we always want to index
      var baseFields = ["uri", "uri_path", "comment"];

      // Auto-detected fields: all keys starting with text_ or title_
      var dynamicFields = [];
      var sample = data[0];

      Object.keys(sample).forEach(function (key) {
        if (/^(text_|title_)/.test(key)) {
          dynamicFields.push(key);
        }
      });

      // Merge and make sure fields are unique
      var allFields = baseFields.concat(
        dynamicFields.filter(function (field) {
          return baseFields.indexOf(field) === -1;
        })
      );

      // ------------------------------------------------------------

      miniSearch = new MiniSearch({
        fields: allFields,
        storeFields: ["url"],
        idField: "url"
      });

      var docs = data
        .filter(function (item) {
          return item.url && elementByUrl.has(item.url);
        })
        .map(function (item) {
          var doc = { url: item.url || "" };

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
      var url = el.getAttribute("data-url");
      if (visibleUrls.has(url)) {
        el.classList.remove("d-none");
      } else {
        el.classList.add("d-none");
      }
    });
  }

  searchInput.addEventListener("input", function () {
    var query = searchInput.value.trim();

    if (!indexReady || !miniSearch || !query) {
      showAll();
      return;
    }

    var results = miniSearch.search(query, {
      prefix: true,
      fuzzy: 0.2
    });

    if (results.length === 0) {
      elements.forEach(function (el) {
        el.classList.add("d-none");
      });
    } else {
      filterByResults(results);
    }
  });
});
