document.addEventListener("DOMContentLoaded", () => {
  const filterInput = document.getElementById("filter")
  if (!filterInput) return

  // Collect all result cards on this page
  const elements = Array.prototype.slice.call(
    document.querySelectorAll(".element[data-uri]")
  )
  if (elements.length === 0) {
    return
  }

  // Map url -> DOM element for quick lookup
  const elementByUri = new Map()
  elements.forEach(element => {
    const url = element.getAttribute("data-uri")
    if (url) {
      elementByUri.set(url, element)
    }
  })

  let miniSearch = null
  let indexReady = false

  // Load index.json from the same directory as this page
  fetch("index.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error("index.json not found for this page")
      }
      return response.json()
    })
    .then((data) => {
      // base fields we always want to index
      const baseFields = ["uri", "uri_path", "comment"]

      // Collect all keys starting with text_ or title_ across ALL items
      const dynamicFieldSet = new Set()

      data.forEach((item) => {
        Object.keys(item).forEach(key => {
          if (/^(text_|title_)/.test(key)) {
            dynamicFieldSet.add(key)
          }
        })
      })

      const dynamicFields = Array.from(dynamicFieldSet)

      // Merge and make sure fields are unique
      const allFields = baseFields.concat(
        dynamicFields.filter((field) => baseFields.indexOf(field) === -1)
      )

      miniSearch = new MiniSearch({
        fields: allFields,
        storeFields: ["uri"],
        idField: "uri"
      })

      const docs = data
        .filter((item) => item.uri && elementByUri.has(item.uri))
        .map((item) => {
          const doc = { uri: item.uri || "" }

          allFields.forEach((field) => {
            // Fall back to empty string if missing / null
            doc[field] = item[field] || ""
          })

          return doc
        })

      miniSearch.addAll(docs)
      indexReady = true
    })
    .catch((err) => console.error("MiniSearch: could not load or build index.json", err))

  const showAll = () => {
    elements.forEach((element) => {
      element.classList.remove("d-none")
    })
  }

  const filterByResults = (results) => {
    const visibleUrls = new Set(results.map((r) => r.id))

    elements.forEach((element) => {
      const url = element.getAttribute("data-uri")
      if (visibleUrls.has(url)) {
        element.classList.remove("d-none")
      } else {
        element.classList.add("d-none")
      }
    })
  }

  const handleInput = (event) => {
    const query = event.target.value.trim()

    if (!indexReady || !miniSearch || !query) {
      showAll()
      return
    }

    const options = {
      prefix: true,
      fuzzy: 0.2
    }

    // if it looks like a URL, search more strictly
    if (/^https?:\/\//.test(query)) {
      options = {
        fields: ["uri", "uri_path", "url"],
        prefix: false,
        fuzzy: false,
        combineWith: "AND"
      }
    }

    const results = miniSearch.search(query, options)

    if (_.isEmpty(results)) {
      elements.forEach((element) => {
        element.classList.add("d-none")
      })
    } else {
      filterByResults(results)
    }
  }

  const debouncedInput = _.debounce(handleInput, 300)

  filterInput.addEventListener("input", debouncedInput)
})


document.addEventListener("DOMContentLoaded", () => {
  const flatView = document.getElementById("catalog-flat-view");
  const treeView = document.getElementById("catalog-tree-view");
  const btnFlat = document.getElementById("btn-view-flat");
  const btnTree = document.getElementById("btn-view-tree");

  // Only run on catalog element pages
  if (!flatView || !treeView || !btnFlat || !btnTree) return;

  const baseUrl = document.body.dataset.baseUrl || "/";
  const rootUri = btnTree.dataset.rootUri;
  let treeLoaded = false;
  let elementByUri = null;

  function setActiveButton(activeBtn) {
    [btnFlat, btnTree].forEach((btn) => btn.classList.remove("active"));
    activeBtn.classList.add("active");
  }

  function showFlat() {
    flatView.classList.remove("d-none");
    treeView.classList.add("d-none");
    setActiveButton(btnFlat);
  }

  function showTree() {
    flatView.classList.add("d-none");
    treeView.classList.remove("d-none");
    setActiveButton(btnTree);
    if (!treeLoaded) {
      loadTree();
    }
  }

  // Keys on the element JSON that represent structural children
  const CHILD_KEYS = ["sections", "pages", "questionsets", "questions"];

  async function loadTree() {
    try {
      const indexUrl = (baseUrl || "/") + "index.json";
      const res = await fetch(indexUrl);
      if (!res.ok) {
        throw new Error("Failed to load index.json");
      }

      const allElements = await res.json();
      elementByUri = new Map(allElements.map((el) => [el.uri, el]));

      const treeRoot = buildTreeForUri(rootUri, elementByUri);
      treeView.innerHTML = "";
      treeView.appendChild(renderTreeNode(treeRoot, baseUrl));
      treeLoaded = true;
    } catch (err) {
      console.error(err);
      treeView.innerHTML =
        '<div class="alert alert-danger">Could not load catalog tree.</div>';
    }
  }

  function buildTreeForUri(uri, byUri, seen = new Set()) {
    const element = byUri.get(uri);
    if (!element || seen.has(uri)) return null;

    seen.add(uri);

    const node = {
      uri: element.uri,
      type: element.type || element.model || "element",
      url: element.url,
      children: [],
    };

    CHILD_KEYS.forEach((key) => {
      const refs = element[key];
      if (Array.isArray(refs)) {
        refs.forEach((ref) => {
          if (ref && ref.uri) {
            const childNode = buildTreeForUri(ref.uri, byUri, seen);
            if (childNode) {
              node.children.push(childNode);
            }
          }
        });
      }
    });

    return node;
  }

  function renderTreeNode(node, baseUrl) {
    if (!node) {
      return document.createTextNode("");
    }

    const wrapper = document.createElement("div");
    wrapper.classList.add("mb-1");

    const header = document.createElement("div");
    header.classList.add("small");

    const label = document.createElement("strong");
    label.textContent = (node.type || "element") + ": ";
    header.appendChild(label);

    if (node.url) {
      const link = document.createElement("a");
      link.href = baseUrl + node.url.replace(/^\//, "");
      link.textContent = node.uri;
      header.appendChild(link);
    } else {
      const span = document.createElement("span");
      span.textContent = node.uri;
      header.appendChild(span);
    }

    wrapper.appendChild(header);

    if (node.children && node.children.length > 0) {
      const ul = document.createElement("ul");
      ul.classList.add("list-unstyled", "ms-3");

      node.children.forEach((child) => {
        const li = document.createElement("li");
        li.appendChild(renderTreeNode(child, baseUrl));
        ul.appendChild(li);
      });

      wrapper.appendChild(ul);
    }

    return wrapper;
  }

  btnFlat.addEventListener("click", (event) => {
    event.preventDefault();
    showFlat();
  });

  btnTree.addEventListener("click", (event) => {
    event.preventDefault();
    showTree();
  });
});
